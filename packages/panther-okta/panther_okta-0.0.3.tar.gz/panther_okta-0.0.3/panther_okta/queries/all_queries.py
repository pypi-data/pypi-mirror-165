from typing import Literal
from panther_config import query

__all__ = [
    "activity_audit",
    "admin_access_granted",
    "mfa_password_reset_audit",
    "session_id_audit",
    "support_access",
]

default_query_schedule = query.IntervalSchedule(
    rate_minutes=43200,
    timeout_minutes=1,
)


def activity_audit(
    datalake: Literal["athena", "snowflake"],
    overrides: query.QueryOptions = query.QueryOptions(),
) -> query.Query:
    """Audit user activity across your environment. Customize to filter on specfic users, time ranges, etc"""

    sql = """
      SELECT actor:displayName AS actor_name, actor:alternateId AS actor_email, eventType, COUNT(*) AS activity_count
      FROM panther_logs.public.okta_systemlog
      WHERE p_occurs_since('7 days')
      AND actor:type = 'User'
      -- Uncomment lines below to filter by user email and/or eventType
      -- and actor_email = 'email'
      -- and eventType = 'eventType'
      GROUP BY actor:displayName, actor:alternateId, eventType
      ORDER BY  actor_name, activity_count DESC
    """

    if datalake == "athena":
        sql = """
          SELECT actor.displayName AS actor_name, actor.alternateId AS actor_email, eventType, COUNT(*) AS activity_count
          FROM panther_logs.okta_systemlog
          WHERE p_occurs_since('7 days')
          AND actor.type = 'User'
          -- Uncomment lines below to filter by user email and/or eventType
          -- and actor_email = '<EMAIL_GOES_HERE>'
          -- and eventType = '<EVENTTYPE_GOES_HERE>'
          GROUP BY actor.displayName, actor.alternateId, eventType
          ORDER BY  actor_name, activity_count DESC
        """

    return query.Query(
        name=(overrides.name or "Okta Investigate User Activity"),
        enabled=(overrides.enabled or True),
        sql=(overrides.sql or sql),
        description=(
            overrides.description
            or "Audit user activity across your environment. Customize to filter on specfic users, time ranges, etc"
        ),
        schedule=(overrides.schedule or default_query_schedule),
    )


def admin_access_granted(
    datalake: Literal["athena", "snowflake"],
    overrides: query.QueryOptions = query.QueryOptions(),
) -> query.Query:
    """Audit instances of admin access granted in your okta tenant"""

    sql = """
      SELECT 
      p_event_time as event_time,
      actor:alternateId as actor_email,
      actor:displayName as actor_name,
      displayMessage,
      eventType,
      debugContext:debugData:privilegeGranted as priv_granted,
      target as target_name,
      client:ipAddress as src_ip,
      client:geographicalContext:city as city,
      client:geographicalContext:country as country,
      client:userAgent:rawUserAgent as user_agent
      FROM 
        panther_logs.public.okta_systemlog
      WHERE 
      ( eventType = 'user.account.privilege.grant' 
       OR 
        eventType = 'group.privilege.grant'
       AND
         debugContext:debugData:privilegeGranted like '%Admin%'
      )
        AND  
        p_occurs_between('2022-01-14','2022-03-22')
      ORDER BY
      event_time desc
    """

    if datalake == "athena":
        sql = """
          SELECT 
          p_event_time as event_time,
          actor.alternateid as actor_email,
          actor.displayName as actor_name,
          displayMessage,
          eventType,
          json_extract(debugcontext.debugdata, '$.privilegeGranted') as priv_granted,
          target as target_name,
          client.ipAddress as src_ip,
          client.geographicalContext.city as city,
          client.geographicalContext.country as country,
          client.useragent.rawUserAgent as user_agent
          FROM panther_logs.okta_systemlog
          WHERE 
          (
          eventType = 'user.account.privilege.grant' OR 
          eventType = 'group.privilege.grant' AND
          cast(json_extract(debugcontext.debugdata, '$.privilegeGranted') as varchar) LIKE '%Admin%'
          ) AND
          p_occurs_between('2022-01-14','2022-03-22')
          ORDER BY
          event_time desc
        """

    return query.Query(
        name=(overrides.name or "Okta Admin Access Granted"),
        enabled=(overrides.enabled or True),
        sql=(overrides.sql or sql),
        description=(
            overrides.description
            or "Audit instances of admin access granted in your okta tenant"
        ),
        schedule=(overrides.schedule or default_query_schedule),
    )


def mfa_password_reset_audit(
    datalake: Literal["athena", "snowflake"],
    overrides: query.QueryOptions = query.QueryOptions(),
) -> query.Query:
    """Investigate Password and MFA resets for the last 7 days"""

    sql = """
      SELECT p_event_time,actor:alternateId as actor_user,target[0]:alternateId as target_user, eventType,client:ipAddress as ip_address
      FROM panther_logs.public.okta_systemlog
      WHERE eventType IN ('user.mfa.factor.reset_all', 'user.mfa.factor.deactivate', 'user.mfa.factor.suspend', 'user.account.reset_password', 'user.account.update_password','user.mfa.factor.update')
      and p_occurs_since('7 days')
      -- If you wish to investigate an indvidual user , uncomment this line and add their email here  
      -- and actor:alternateId = '<EMAIL_GOES_HERE>'
      ORDER by p_event_time DESC
    """

    if datalake == "athena":
        sql = """
          SELECT p_event_time,actor.alternateId as actor_user,target[1].alternateId as target_user, eventType,client.ipAddress as ip_address
          FROM panther_logs.okta_systemlog
          WHERE eventType IN ('user.mfa.factor.reset_all', 'user.mfa.factor.deactivate', 'user.mfa.factor.suspend', 'user.account.reset_password', 'user.account.update_password')
          and p_occurs_since('7 days')
          -- If you wish to investigate an indvidual user , uncomment this line and add their email here  
          -- and actor:alternateId = '<EMAIL_GOES_HERE>'
          ORDER by p_event_time DESC
        """

    return query.Query(
        name=(overrides.name or "Okta Investigate MFA and Password resets"),
        enabled=(overrides.enabled or True),
        sql=(overrides.sql or sql),
        description=(
            overrides.description
            or "Investigate Password and MFA resets for the last 7 days"
        ),
        schedule=(overrides.schedule or default_query_schedule),
    )


def session_id_audit(
    datalake: Literal["athena", "snowflake"],
    overrides: query.QueryOptions = query.QueryOptions(),
) -> query.Query:
    """Search for activity releated to a specific SessionID in Okta panther_logs.okta_systemlog"""

    sql = """
        SELECT  
          p_event_time as event_time,
          actor:alternateId as actor_email,
          actor:displayName as actor_name,
          authenticationContext:externalSessionId as sessionId,
          displayMessage,
          eventType,
          client:ipAddress as src_ip,
          client:geographicalContext:city as city,
          client:geographicalContext:country as country,
          client:userAgent:rawUserAgent as user_agent
        FROM panther_logs.public.okta_systemlog
        WHERE p_occurs_since('7 days')
        -- Uncomment the line below and replace 'sessionId' with the sessionId you are investigating
        -- and authenticationContext:externalSessionId = '<SESSIONID_GOES_HERE>'
        ORDER BY event_time DESC
    """

    if datalake == "athena":
        sql = """
          SELECT  
            p_event_time as event_time,
            actor.alternateId as actor_email,
            actor.displayName as actor_name,
            authenticationContext.externalSessionId as sessionId,
            displayMessage,
            eventType,
            client.ipAddress as src_ip,
            client.geographicalContext.city as city,
            client.geographicalContext.country as country,
            client.userAgent.rawUserAgent as user_agent
          FROM panther_logs.okta_systemlog
          WHERE p_occurs_since('7 days')
          -- Uncomment the line below and replace 'sessionId' with the sessionId you are investigating
          -- and authenticationContext:externalSessionId = '<SESSIONID_GOES_HERE>'
            ORDER BY event_time DESC

        """

    return query.Query(
        name=(overrides.name or "Okta Investigate Session ID Activity"),
        enabled=(overrides.enabled or True),
        sql=(overrides.sql or sql),
        description=(
            overrides.description
            or "Search for activity releated to a specific SessionID in Okta panther_logs.okta_systemlog"
        ),
        schedule=(overrides.schedule or default_query_schedule),
    )


def support_access(
    datalake: Literal["athena", "snowflake"],
    overrides: query.QueryOptions = query.QueryOptions(),
) -> query.Query:
    """Show instances that Okta support was granted to your account"""

    sql = """
      SELECT 
      p_event_time as event_time,
      actor:alternateId as actor_email,
      actor:displayName as actor_name,
      client:ipAddress as src_ip,
      client:geographicalContext:city as city,
      client:geographicalContext:country as country,
      client:userAgent:rawUserAgent as user_agent,
      displayMessage,
      eventType
      FROM
      panther_logs.public.okta_systemlog
      WHERE 
        eventType = 'user.session.impersonation.grant' 
        OR 
        eventType = 'user.session.impersonation.initiate'
       AND  
          p_occurs_between('2022-01-14','2022-03-22')
      ORDER BY
        event_time desc
    """

    if datalake == "athena":
        sql = """
          SELECT 
          p_event_time as event_time,
          actor.alternateid as actor_email,
          actor.displayName as actor_name,
          displayMessage,
          eventType,
          client.ipAddress as src_ip,
          client.geographicalContext.city as city,
          client.geographicalContext.country as country,
          client.useragent.rawUserAgent as user_agent
          FROM panther_logs.okta_systemlog
          WHERE 
          (
          eventType = 'user.session.impersonation.grant' OR 
          eventType = 'user.session.impersonation.initiate'
          ) and
          p_occurs_between('2022-01-14','2022-03-22')
          ORDER BY
            event_time desc
        """

    return query.Query(
        name=(overrides.name or "Okta Support Access"),
        enabled=(overrides.enabled or True),
        sql=(overrides.sql or sql),
        description=(
            overrides.description
            or "Show instances that Okta support was granted to your account"
        ),
        schedule=(overrides.schedule or default_query_schedule),
    )
