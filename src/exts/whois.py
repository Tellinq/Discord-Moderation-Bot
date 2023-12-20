import disnake
from disnake.ext import plugins


plugin = plugins.Plugin()


@plugin.slash_command()
async def whois(inter: disnake.CmdInter, target: disnake.User):
    
    """
    Get details about a user/member

    Parameters
    ----------
    target: The user/member to get details of
    """
    
    embed = disnake.Embed()
    embed.set_author(name=f"{target}", icon_url=target.display_avatar)
    embed.set_thumbnail(target.display_avatar)
    
    embed.add_field(
        "ID",
        target.id,
        inline=False
    )
    
    embed.add_field(
        "Creation Date",
        disnake.utils.format_dt(target.created_at, "R"),
        inline=False
    )
    
    if isinstance(target, disnake.Member):
        embed.add_field(
            "Join Date",
            disnake.utils.format_dt(target.joined_at, "R"),
            inline=False
        )
        
        roles = target.roles[1:] # exclude @everyone
        
        if len(roles) > 0:
            embed.add_field(
                f"Roles [{len(roles)}]",
                "".join(role.mention for role in roles),
                inline=False
            )
        
    await inter.send(embed=embed)
    
    
setup, teardown = plugin.create_extension_handlers()